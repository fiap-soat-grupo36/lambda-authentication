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

# Create an isolated build directory where we'll install dependencies and copy code
BUILD_DIR="$APP_DIR/build"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# If requirements exist in the app dir, install them into the build dir so they are
# bundled with the lambda. Use the system python3's pip to avoid relying on 'pip'.
if [ -f "$APP_DIR/requirements.txt" ]; then
	echo "Installing Python dependencies from $APP_DIR/requirements.txt into build dir"
	if command -v python3 >/dev/null 2>&1; then
		PYEXEC=python3
	elif command -v python >/dev/null 2>&1; then
		PYEXEC=python
	else
		echo "ERROR: python is not installed or not in PATH" >&2
		exit 1
	fi

	# Install requirements into the isolated build directory. This may take a moment.
	"$PYEXEC" -m pip install --upgrade pip >/dev/null
	"$PYEXEC" -m pip install -r "$APP_DIR/requirements.txt" -t "$BUILD_DIR" --upgrade >/dev/null
else
	echo "No requirements.txt found in $APP_DIR — packaging only handler.py"
fi

# Copy the handler (and any local code) into build dir
echo "Copying handler into build dir"
cp "$APP_DIR"/handler.py "$BUILD_DIR"/

# Create the zip from the contents of build dir so that site-packages and handler
# are at the root of the archive (Lambda expects packages next to handler file).
pushd "$BUILD_DIR" > /dev/null
zip -r9 "$ZIP_PATH" . >/dev/null
popd > /dev/null

# Clean up build dir
rm -rf "$BUILD_DIR"

echo "Packaged: $ZIP_PATH"
