import clean
import json2ppt

if __name__ == "__main__":
    clean.main()
    json2ppt.create_ppt_from_json("content.json", "output_ai.pptx")