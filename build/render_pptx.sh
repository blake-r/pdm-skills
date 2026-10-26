#!/bin/bash
# usage: render_pptx.sh in.pptx name
# Renders a PPTX to PNG slides through Keynote (macOS). Output goes to $RENDER_OUT/<name>
# (default: /tmp/pdm-render/<name>).
S="${RENDER_OUT:-/tmp/pdm-render}"
mkdir -p "${S:?}/${2:?}"; rm -f "${S:?}/${2:?}"/*
osascript <<OSA
tell application "Keynote"
  set d to open POSIX file "$1"
  export d to POSIX file "$S/$2" as slide images with properties {image format:PNG}
  close d saving no
end tell
OSA
ls "$S/$2"
