#!/usr/bin/env
from datetime import datetime, timedelta
from flask import Flask

from .routes import api_routes, view_routes
from. config import ProductionConfig, DevelopmentConfig, TestingConfig
from .utils import duration_to_time

def create_app():
    # Create Flask App
    app = Flask(__name__)
    app.register_blueprint(api_routes)
    app.register_blueprint(view_routes)

    # Load Configuration
    if app.testing:
        app.config.from_object(TestingConfig())
    if app.debug:
        app.config.from_object(DevelopmentConfig())
    else:
        app.config.from_object(ProductionConfig())

    # @app.teardown_appcontext
    # def close_connection(exception):
    #     Database.close()
    
    # JINJA Template Filters
    @app.template_filter('dt')
    def filter_time_to_date(s):
        return datetime.fromtimestamp(int(s)).strftime('%b %d, %Y %I:%M %p')

    @app.template_filter('seconds')
    def filter_seconds_timedelta(s):
        return timedelta(seconds=int(s))

    @app.template_filter('duration')
    def filter_duration_to_time(s):
        return duration_to_time(s)

    @app.template_filter('audio')
    def filter_mpd_audio_str(s):
        '''Converts MPD audio string "441000:24:2" to "44.1 kHz | 24 bit"'''
        audio = s.split(':')
        hz = str(int(audio[0])/1000)
        return hz + ' kHz / ' + audio[1] + ' bit'
        return timedelta(seconds=int(s))

    return app