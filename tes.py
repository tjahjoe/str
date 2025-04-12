from model_genai import ModelGenai

model = ModelGenai()
result_stream = model.chain.stream({'input': 'halo'})

for chunk in result_stream:
    print(chunk, end="", flush=True)
print()