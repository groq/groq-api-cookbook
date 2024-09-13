from jigsawstack import JigsawStack
from fire import Fire


jigsaw = JigsawStack(api_key="your-api-key")


def main() -> None:

    #  Create prompt

    params = {
        "prompt": "How to cook {dish}",  # The prompt for your use case
        "inputs": [{"key": "dish"}],  # dynamic vars that are in the brackets {}
        "return_prompt": [
            {
                "step": "Name of this step",
                "details": "Details of this step",
            }
        ],  # The structure of the JSON, in this case, an array of objects
    }

    result = jigsaw.prompt_engine.create(params)

    # Run the prompt

    resp = jigsaw.prompt_engine.run(
        {
            "id": result.prompt_engine_id,  # The ID you got after creating the engine
            "input_values": {
                "dish": "Singaporean chicken rice",  # They value for your dynamic field
            },
        }
    )

    # Print the result
    print(resp)
    pass


if __name__ == "__main__":
    Fire(main)
