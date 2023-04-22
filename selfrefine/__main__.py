import os
from pprint import pprint
from functools import lru_cache

import openai
import json
import random
from dotenv import load_dotenv
from google.cloud import translate
import percache

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
GOOGLE_TRANSLATE_PROJECT_ID = os.getenv("GOOGLE_TRANSLATE_PROJECT_ID")

cache = percache.Cache('my-cache')

@cache
def translate_text(text, project_id=GOOGLE_TRANSLATE_PROJECT_ID):

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": "ja",
        }
    )

    result = []
    for translation in response.translations:
        result.append(translation.translated_text)

    return "".join(result)

@cache
def chat_async(messages, stop=[], model="gpt-4"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        stream=True,
    )
    ans = []
    print("\n💻 Agent: ")
    print("====messages====")
    print(messages)
    print()
    for chunk in response:
        content = chunk["choices"][0]["delta"].get("content", "")
        print(content, end="")
        ans.append(content)
    ans = "".join(ans).strip()
    return ans

def parse_answer(answer_text):
    try:
        sub_answer_text = answer_text.split("<OUT />")[-1]
        answer = json.loads(sub_answer_text)
        return answer
    except json.decoder.JSONDecodeError:
        print("JSONDecodeError")
    
    try:
        sub_answer_text = answer_text.split("<OUT>")[-1]
        answer = json.loads(sub_answer_text)
        return answer
    except json.decoder.JSONDecodeError:
        print("JSONDecodeError")
    
    try:
        sub_answer_text = answer_text.split("<OUT>")[0]
        answer = json.loads(sub_answer_text)
        return answer
    except json.decoder.JSONDecodeError:
        print("JSONDecodeError")

    try:
        sub_answer_text = answer_text.split("<OUT />")[0]
        answer = json.loads(sub_answer_text)
        return answer
    except json.decoder.JSONDecodeError:
        print("JSONDecodeError")

    try:
        sub_answer_text = answer_text.strip()
        answer = json.loads(sub_answer_text)
        return answer
    except json.decoder.JSONDecodeError:
        print("JSONDecodeError")

    try:
        # <OUT> と </OUT> で囲まれた部分を取り出す
        sub_answer_text = answer_text.split("<OUT>")[1].split("</OUT>")[0]
        answer = json.loads(sub_answer_text)
        return answer
    except IndexError:
        print("IndexError")
    except json.decoder.JSONDecodeError:
        print("JSONDecodeError")

    raise Exception("Failed to parse answer_text")


initial_answer = """
Title: Advanced IPA Parsing from Images for Linguistic Applications: A Comprehensive Methodology and Technical Components - Revised Proposal

1. Introduction

This revised proposal addresses the initial instructions and incorporates valuable feedback. We provide a more comprehensive overview, with detailed explanations of terminology and methods, and stronger links between sections. We also include more specific references to relevant research and literature, clarifying budget estimates and timetable, and identifying clear evaluation criteria.

1.1. Objective and Target: Developing an advanced IPA parsing method
1.2. Existing Systems and Literature: Review of related work in text recognition and IPA parsing
1.3. Proposed Methodology and Technical Components: Technical components for IPA parsing, supported by research and literature
1.4. Implementation and Scope: Details on the proposed technique's implementation and applicability
1.5. Practicality and Benefits: Discussing practical implications and advantages resulting from implementation
1.6. Resources, Technologies, and Evaluation: Specific tools, libraries, and evaluation methods to be employed
1.7. Budget Breakdown: Itemized list of estimated costs for resources, personnel, and data
1.8. Timetable and Milestones: Project phases and key deliverables for monitoring
1.9. Conclusion: Concrete achievements and evaluation methodology, potential impact of the project

1.2. Existing Systems and Literature

Optical Character Recognition (OCR) systems have been widely used for text recognition tasks, and OCR engines like Tesseract, CuneiForm, and ABBYY FineReader demonstrate varying performance in multiple languages and scripts (Smith, 2007; Volk et al., 2010). However, IPA symbols present unique challenges. The importance of tailored solutions is emphasized by Gauthier et al. (2016), which developed an OCR engine for the UNIMARC bibliographic format, containing numerous IPA symbols.

1.3. Proposed Methodology and Technical Components

1) Preprocessing
2) Segmentation
3) Feature Extraction
4) Classification
5) IPA-specific Strategies

4. Implementation and Scope

Using Python, we will primarily use TensorFlow and OpenCV for image processing and deep learning tasks. We intend to train our models using a large dataset of IPA images, sourced from IPA databases, online resources, and scanned textbooks. Applicability will be tested across various image types and scenarios, ensuring effectiveness in real-world applications and accommodating different linguistic research and learning use cases.

5. Practicality and Benefits

Successful implementation of the proposed method provides numerous practical benefits:

- Enhancing linguistic analysis by efficiently processing large volumes of IPA data from diverse sources.
- Assisting language learners and educators by simplifying access to IPA information.
- Improving performance of natural language processing and speech synthesis systems by providing reliable IPA input.

6. Resources, Technologies, and Evaluation (Refer to the original report for details)

7. Budget Breakdown

- Personnel: $100,000 (includes salaries for developers, researchers, and project manager)
- Data Acquisition and Storage: $10,000
- Computational Resources: $20,000 (includes cloud-based GPU resources for training deep learning models)
- Miscellaneous Expenses: $5,000
Total Estimated Budget: $135,000

8. Timetable and Milestones

Month 1-3: Preprocessing and segmentation development
Month 4-6: Feature extraction and classification model development
Month 7-9: IPA-specific strategies implementation and system integration
Month 10-12: Final testing, evaluation, and deployment

9. Conclusion

Upon successful implementation, we aim to achieve:

- High accuracy and efficiency in IPA parsing from images.
- Better understanding and expansion of deep learning techniques for similar linguistic problems.
- A positive impact on research and learning in phonetics, speech sciences, and natural language processing.

By providing stronger links, more detailed literature references, specific budget estimates and timetable, and clear evaluation criteria, this revised proposal demonstrates the project's validity and necessity. We seek funding and approval to advance the project and create a lasting impact in linguistic research and learning.
"""

def main():
    max_iteration: int = 100
    input_x = "Please be as specific as possible in proposing the most appropriate method for parsing the International Phonetic Alphabet from an image containing the International Phonetic Alphabet and summarize it in a technical report. For each phase, please also provide several alternatives and a rational explanation of why you have chosen the proposed method. This study has not yet begun and this report will be used for the purpose of making a proposal to obtain funding and estimate budget. Language of output should be in English."
    print(translate_text(input_x))

    global initial_answer

    output_history = []

    frozen_messages = [{"role": "user", "content": input_x}]
    messages = [x for x in frozen_messages]
    if not initial_answer:
        answer_text = chat_async(messages=messages)
    else:
        answer_text = initial_answer

    print(f"==== Iteration 0 ====")
    print(f"==== Answer ====")
    print(answer_text)
    print(translate_text(answer_text))

    messages += [{"role": "assistant", "content": answer_text}]
    messages += [{"role": "user", "content": """上記の出力を批判的に評価し、改善のアドバイスを以下のJSON形式で出力してください。<OUT />{"feedback":"批評と改善してほしい点", "current_score": フィードバック前の文章の0.0-10.0までの点数}"""}]
    while True:
        try:
            feedback_text = chat_async(messages=messages)
            parsed_feedback = parse_answer(feedback_text)
            assert "current_score" in parsed_feedback and "feedback" in parsed_feedback
            break
        except:
            print(feedback_text)
            print("retrying...")    

    messages = [x for x in frozen_messages]
    messages += [{"role": "assistant", "content": answer_text}]
    messages += [{"role": "user", "content": """この文章のスコアは """ + str(parsed_feedback["current_score"]) + """ 点です。当初の指示と、以下のフィードバックをもとに、書き直してください。フィードバック: """ + str(parsed_feedback["feedback"]) + """
書き直した回答を出力してください。"""}]
    feedback_text = chat_async(messages=messages)
    print("==== Answer ====")
    print(feedback_text)
    print(translate_text(feedback_text))

    for i_iteration in range(max_iteration):
        print(f"==== Iteration {i_iteration} ====")
        messages = [x for x in frozen_messages]
        messages += [{"role": "assistant", "content": answer_text}]
        messages += [{"role": "user", "content": """上記の出力を批判的に評価し、改善のアドバイスを以下のJSON形式で出力してください。<OUT />{"feedback":"批評と改善してほしい点", "current_score": フィードバック前の文章の0.0-10.0までの点数}"""}]

        while True:
            try:
                feedback_text = chat_async(messages=messages)
                parsed_feedback = parse_answer(feedback_text)
                assert "current_score" in parsed_feedback and "feedback" in parsed_feedback
                break
            except:
                print(feedback_text)
                print("retrying...")

        messages = [x for x in frozen_messages]
        messages += [{"role": "assistant", "content": answer_text}]
        messages += [{"role": "user", "content": """この文章のスコアは """ + str(parsed_feedback["current_score"]) + """ 点です。当初の指示と、以下のフィードバックをもとに、書き直してください。フィードバック: """ + str(parsed_feedback["feedback"]) + """
書き直した回答を出力してください。"""}]
        answer_text = chat_async(messages=messages)

        # 現在の出力
        print("==== Current Output ====")
        print(answer_text)
        print(translate_text(answer_text))
        print()

        output_history.append({
            "text": answer_text,
            "translated_text": translate_text(answer_text),
            "feedback": parsed_feedback["feedback"],
            "score": parsed_feedback["current_score"],
            })

        with open("output_history.json", "w", encoding="utf-8") as f:
            # human readable json
            json.dump(output_history, f, indent=2, ensure_ascii=False)
        with open("last_output.txt", "w", encoding="utf-8") as f:
            f.write(answer_text)
        with open("last_output_ja.txt", "w", encoding="utf-8") as f:
            f.write(translate_text(answer_text))

        print("==== Output History ====")
        pprint(output_history)


if __name__ == "__main__":
    main()
