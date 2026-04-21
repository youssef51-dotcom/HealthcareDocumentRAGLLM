import json
import time
from pydantic import ValidationError
from llm.prompts import build_extraction_prompt, build_repair_prompt
from llm.provider_factory import get_provider
from models.schema import ClinicalData
from utils.logger import log
from utils.validation import format_pydantic_errors


MAX_RETRIES = 2


def extract_structured_data(text: str, provider_name: str) -> dict:
    total_start = time.time()
    provider = get_provider(provider_name)

    # ---------------- INITIAL PROMPT ----------------
    t0 = time.time()
    prompt = build_extraction_prompt(text)
    t_build_extraction_prompt = time.time() - t0
    log("build_extraction_prompt TIME; ", t_build_extraction_prompt)
    print(f"build_extraction_prompt Completed in {t_build_extraction_prompt:.2f}s")
    log("INITIAL PROMPT", prompt)

    t0 = time.time()
    output = provider.generate(prompt)
    t_generate = time.time() - t0
    log("provider generate TIME; ", t_generate)
    print(f"provider generate Completed in {t_generate:.2f}s")
    log("RAW OUTPUT", output)

    t0 = time.time()
    # ---------------- MAIN LOOP ----------------
    for attempt in range(MAX_RETRIES + 1):
        try:
            data = json.loads(output)
        except Exception as e:
            log("JSON ERROR", str(e))
            data = {}

        # ---------------- VALIDATION ----------------
        try:
            validated = ClinicalData(**data)

            if (
                    validated.diagnosis is None and
                    not validated.findings and
                    validated.treatment is None
            ):
                raise ValidationError("Empty extraction", model=ClinicalData)
            print("VALIDATION SUCCESS", validated.model_dump())
            log("VALIDATION SUCCESS", validated.model_dump())

            # ---------------- FINAL FALLBACK (SAFETY NET) ----------------
            final_data = validated.model_dump()

            if final_data.get("patient") is None:
                final_data["patient"] = {
                    "age": None,
                    "sex": None
                }

            t_validationAndRepair = time.time() - t0
            log("validation and repair TIME; ", t_validationAndRepair)
            print(f"validation and repair Completed in {t_validationAndRepair:.2f}s")
            total_time = time.time() - total_start
            log("TOTAL TIME: ", total_time)

            print(f"[SUCCESS] Completed in {total_time:.2f}s")

            return final_data

        except ValidationError as e:
            log("VALIDATION ERROR", str(e))

            # ---------------- STOP IF MAX RETRIES ----------------
            if attempt == MAX_RETRIES:
                print("[ERROR] Max retries reached")

                # FINAL FALLBACK (last resort)
                if data.get("patient") is None:
                    data["patient"] = {
                        "age": None,
                        "sex": None
                    }

                return data

            # ---------------- REPAIR STEP ----------------
            errors = format_pydantic_errors(e.errors())
            repair_prompt = build_repair_prompt(text, data,errors)
            log("REPAIR PROMPT", repair_prompt[:2000])

            output = provider.generate(repair_prompt)
            log("REPAIR OUTPUT", output)

    return {"error": "unexpected failure"}