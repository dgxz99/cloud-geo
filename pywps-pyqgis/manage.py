from app import create_app
import argparse

parser = argparse.ArgumentParser(description='Run Flask app with specific configuration.')
parser.add_argument('--deploy_mode', help='Deployment mode (e.g., single, distributed)')

args = parser.parse_args()
config_params = {
    'deploy_mode': args.deploy_mode,
}

app = create_app(config_params)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
