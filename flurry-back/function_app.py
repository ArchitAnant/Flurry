import azure.functions as func
import json
import logging
from utils.trend_builder import get_trends
from utils.script_synthesiser import generate_script
from utils.audio_synthesizer import synthesize_audio
from dotenv import load_dotenv
from utils.trends_storage import get_trend_data,set_trend_data
import datetime

load_dotenv()

app = func.FunctionApp()

@app.route(route="trending", auth_level=func.AuthLevel.FUNCTION)
def trending(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger for fetching trends.')
    try:
        data = get_trend_data()
        
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

@app.route(route="getScript", auth_level=func.AuthLevel.FUNCTION)
def script(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger for fetching scripts.')
    try:
        trend = req.params.get('trend')
        if not trend:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'trend' parameter"}),
                status_code=400,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )
        print("topic: ",trend)
        script = generate_script(trend)
        if not script:
            return func.HttpResponse(
                json.dumps({"error": "No script found"}),
                status_code=404,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )
        return func.HttpResponse(
            json.dumps(script),
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
    
@app.route(route="getAudio", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def getAudio(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger for fetching audio.')
    try:
        body = req.get_json()
        script = body.get('script')
        voice_code = body.get('voice')

        headers = {
        "Access-Control-Allow-Origin": "*",  # Replace * with a specific domain if needed
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "Content-Type"
    }


        if not script:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'script' parameter"}),
                status_code=400,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )
        if voice_code is None:
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

    
@app.route(route="setTrending", auth_level=func.AuthLevel.FUNCTION)
def setTrends(req: func.HttpRequest) :
    logging.info('Manual trigger for setting trends.')
    try:
        set_trend_data(get_trends())
        return func.HttpResponse(
            json.dumps({"message": "Trends updated successfully"}),
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
    
@app.function_name(name="trendstimer")
@app.timer_trigger(schedule="0 0 */12 * * *",  
                   arg_name="trendstimer",
                   run_on_startup=True) 
def set_trends(trendstimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.now(datetime.timezone.utc).replace(
        tzinfo=datetime.timezone.utc).isoformat()
    logging.info('Setting Trends : %s', utc_timestamp)
    try:
        get_trends()
        logging.info("Trends set successfully.")
    except Exception as e:
        logging.error(f"Error setting trends: {e}")
        raise