from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import openai
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
import json
openai.api_key = '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'

def get_caption(img):
     
    # unconditional image captioning
    raw_image = Image.open(img).convert('RGB')

    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

def get_hashtags(caption):
    # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
    
    pre_prompt = "Hey your job is to generate top 10 latest trendy hashtags related to the following image caption.\n\n"

    caption_prompt = "Here is the caption\n\n ^^^\n" + caption + "\n^^^"

    output_format = '''
        Give Prompt's output in the following Json format:
        {
            "hashtags" = [hashtag1, hashtag2, ...]
        }
        
    '''

    main_prompt = pre_prompt + caption_prompt + output_format

    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are an instagram hashtag generator from image caption"},
                {"role": "user", "content": main_prompt}
            ]
    )

    textual_output = output['choices'][0]['message']['content']

    json_output = ''
    flag = False

    for c in textual_output:
        if c == '{':
            flag = True
        if flag:
            json_output += c
        if c == '}':
            break
    
    out_object = json.loads(json_output)

    return out_object['hashtags']
