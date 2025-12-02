#!/usr/bin/env bash
set -euo pipefail
# Packages the lambda code into app/lambda.zip or lambda_app/lambda.zip
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Detect app directory (support both 'app' and 'lambda_app')
if [ -d "$ROOT_DIR/app" ]; then
	APP_DIR="$ROOT_DIR/app"
elif [ -d "$ROOT_DIR/lambda_app" ]; then
	APP_DIR="$ROOT_DIR/lambda_app"
else
	echo "ERROR: could not find 'app' or 'lambda_app' directory" >&2
	exit 1
fi

ZIP_PATH="$APP_DIR/lambda.zip"

echo "Packaging lambda from $APP_DIR into $ZIP_PATH"
rm -f "$ZIP_PATH"
pushd "$APP_DIR" > /dev/null
zip -r9 "$ZIP_PATH" handler.py >/dev/null
popd > /dev/null
echo "Packaged: $ZIP_PATH"
