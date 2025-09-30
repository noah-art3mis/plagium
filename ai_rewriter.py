from langchain.chat_models import init_chat_model
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate


def get_data(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


def get_prompt(template_string: str, snippet: str) -> PromptValue:

    if "{text}" not in template_string:
        raise ValueError("Prompt template must contain {text}")

    prompt_template = PromptTemplate.from_template(template_string)
    return prompt_template.invoke({"text": snippet})


def llm(model_name: str, prompt: PromptValue, temperature: float) -> str:
    model = init_chat_model(model=model_name, temperature=temperature)
    response = model.invoke(prompt)

    if isinstance(response.content, str):
        return response.content
    else:
        raise ValueError("Response is not a string", response)


def rewrite(prompt_template: str, snippet: str, model: str, temperature: float) -> str:
    prompt = get_prompt(prompt_template, snippet)
    return llm(model, prompt, temperature)
