import traceback

from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
	PromptTemplate,
)
from pydantic import BaseModel, Field

load_dotenv()

model_name = "text-davinci-003"
temperature = 0.0
model = OpenAI(model_name=model_name, temperature=temperature)


class WeatherRequest(BaseModel):
	setup: str = Field(description="user question")
	city: str = Field(description="city: str = Field(description="name of the city to get weather information, be sure to translate it to English")")


def get_city(user_query: str):
	parser = PydanticOutputParser(pydantic_object=WeatherRequest)
	prompt = PromptTemplate(
		template="Answer the user query.\n{format_instructions}\n{query}\n",
		input_variables=["query"],
		partial_variables={"format_instructions": parser.get_format_instructions()},
	)

	_input = prompt.format_prompt(query=user_query)
	try:
		output = model(_input.to_string())
		response: WeatherRequest = parser.parse(output)

		print(f"setup = {response.setup}")
		print(f"city = {response.city}")

		return response.city
	except Exception as e:
		traceback.print_exc()
		return 'Shanghai'
