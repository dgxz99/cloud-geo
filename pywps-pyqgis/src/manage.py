import argparse
import os

parser = argparse.ArgumentParser(description='Run Flask app with specific configuration.')
parser.add_argument('--deploy_mode', help='Deployment mode (e.g., single, distributed)')
parser.add_argument('--work_dir', help='Working directory for the application', default=os.path.dirname(os.path.dirname(__file__)))

args = parser.parse_args()
if args.work_dir is not None:
	os.chdir(args.work_dir)

from app import create_app

config_params = {
	'deploy_mode': args.deploy_mode,
}

app = create_app(config_params)

if __name__ == "__main__":
	app.run()
