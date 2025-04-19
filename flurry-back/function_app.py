import azure.functions as func
import json
import logging
from utils.trend_builder import get_trends
# from utils.script_synthesiser import generate_script
from utils.audio_synthesizer import synthesize_audio
from dotenv import load_dotenv

load_dotenv()

app = func.FunctionApp()
# world, business, technology, entertainment, sports, science 
@app.route(route="trending", auth_level=func.AuthLevel.FUNCTION)
def trending(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger for fetching trends.')
    try:
        with open("trends.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not data:
            return func.HttpResponse(
                json.dumps({"error": "No data found"}),
                status_code=404,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )
        
        return func.HttpResponse(
            json.dumps(data),
            status_code=200,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )
        
    except Exception as e:
        return func.HttpResponse(
                json.dumps({"error": f"Internal Server Error: {str(e)}"}),
                status_code=500,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )

# @app.route(route="getScript", auth_level=func.AuthLevel.FUNCTION)
# def script(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger for fetching scripts.')
#     try:
#         trend = req.params.get('trend')
#         if not trend:
#             return func.HttpResponse(
#                 json.dumps({"error": "Missing 'trend' parameter"}),
#                 status_code=400,
#                 mimetype="application/json",
#                 headers={"Access-Control-Allow-Origin": "*"}
#             )
#         script = generate_script(trend)
#         if not script:
#             return func.HttpResponse(
#                 json.dumps({"error": "No script found"}),
#                 status_code=404,
#                 mimetype="application/json",
#                 headers={"Access-Control-Allow-Origin": "*"}
#             )
#         return func.HttpResponse(
#             json.dumps(script),
#             status_code=200,
#             mimetype="application/json",
#             headers={"Access-Control-Allow-Origin": "*"}
#         )
    
#     except Exception as e:
#         return func.HttpResponse(
#                 json.dumps({"error": f"Internal Server Error: {str(e)}"}),
#                 status_code=500,
#                 mimetype="application/json",
#                 headers={"Access-Control-Allow-Origin": "*"}
#             )

@app.route(route="getAudio", auth_level=func.AuthLevel.FUNCTION)
def getAudio(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger for fetching world trends.')
    try:
        script = req.params.get('script')
        voice_code = req.params.get('voice')

        if not script:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'script' parameter"}),
                status_code=400,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )
        if not voice_code:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'voice' parameter"}),
                status_code=400,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )

        file_path = synthesize_audio(script, int(voice_code))
        if not file_path:
            return func.HttpResponse(
                json.dumps({"error": "No audio found"}),
                status_code=404,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )
        
        with open(file_path, "rb") as wav_file:
            data = wav_file.read()

        return func.HttpResponse(
            body=data,
            status_code=200,
            mimetype="audio/wav",
            headers={
                "Content-Disposition": "inline; filename=output.wav",
                "Access-Control-Allow-Origin": "*"
            }
        )
    except Exception as e:
        return func.HttpResponse(
                json.dumps({"error": f"Internal Server Error: {str(e)}"}),
                status_code=500,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )