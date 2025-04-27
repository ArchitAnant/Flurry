import azure.functions as func
import json
import logging
from utils.trend_builder import get_trends
from utils.script_synthesiser import generate_script
from utils.audio_synthesizer import synthesize_audio
from dotenv import load_dotenv
from utils.trends_storage import get_trend_data,set_trend_data
from utils.image_trend import evaluate_image
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
    
@app.route(route="getImageResult", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.FUNCTION)
def getImageData(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger for fetching image data.')

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    # Handle preflight (CORS) request
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=200,
            headers=headers
        )

    try:
        body = req.get_json()
        url = body.get('url')

        if not url:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'url' parameter"}),
                status_code=400,
                mimetype="application/json",
                headers=headers
            )
        img_result = evaluate_image(url)
        script = generate_script(img_result.get('description'))


        result = {
            "famous_people": img_result.get('famous_people'),
            "famous_places": img_result.get('famous_places'),
            "text_in_image": img_result.get('text_in_image'),
            "short_script": script.get('short_script'),
            "long_script": script.get('long_script'),
            "hook_topics": script.get('hook_topics')
        }

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json",
            headers=headers
        )
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON format"}),
            status_code=400,
            mimetype="application/json",
            headers=headers
        )
    
    
@app.route(route="getAudio", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.FUNCTION)
def getAudio(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger for fetching audio.')
    
    if req.method == "OPTIONS":
        # Handle CORS preflight request
        return func.HttpResponse(
            "",  # Empty body for OPTIONS response
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",  # Replace * with a specific domain if needed
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        )

    try:
        # Handle the POST request
        body = req.get_json()
        script = body.get('script')
        voice_code = body.get('voice')

        # Set CORS headers for the response
        cors_headers = {
            "Access-Control-Allow-Origin": "*",  # Replace * with a specific domain if needed
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }

        if not script:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'script' parameter"}),
                status_code=400,
                mimetype="application/json",
                headers=cors_headers
            )

        if voice_code is None:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'voice' parameter"}),
                status_code=400,
                mimetype="application/json",
                headers=cors_headers
            )

        file_path = synthesize_audio(script, int(voice_code))
        
        if not file_path:
            return func.HttpResponse(
                json.dumps({"error": "No audio found"}),
                status_code=404,
                mimetype="application/json",
                headers=cors_headers
            )
        
        with open(file_path, "rb") as wav_file:
            data = wav_file.read()

        # Set the CORS headers along with the response
        return func.HttpResponse(
            body=data,
            status_code=200,
            mimetype="audio/wav",
            headers={
                "Content-Disposition": "inline; filename=output.wav",
                **cors_headers  # Merge CORS headers into the response headers
            }
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Internal Server Error: {str(e)}"}),
            status_code=500,
            mimetype="application/json",
            headers=cors_headers
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
                   run_on_startup=False) 
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