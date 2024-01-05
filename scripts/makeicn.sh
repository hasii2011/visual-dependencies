#!/usr/bin/env bash
#
#  The generated .icns file is copied to ${ICON_DIR}
#
# https://gist.github.com/jamieweavis/b4c394607641e1280d447deed5fc85fc
#
#  Embed one icon as the splash image as follows:
#
#  img2py -n embeddedImage -i dependencies-128.png DependencySplash.py
#
if [ -z "$PROJECTS_BASE" ]; then
    echo "You need to set PROJECTS_BASE"
    exit 1
fi
if [ -z "$PROJECT" ]; then
    echo "You need to set PROJECT"
    exit 1
fi

export FULL_PATH="${PROJECTS_BASE}/${PROJECT}"
export ICON_DIR="${FULL_PATH}/visualdependencies/resources/icons"
export BASE_NAME="dependencies-"

ICON_SET_DIR='VisualDependencies.iconset'
GENERATED_MAC_ICON="VisualDependencies.icns"

rm -rf    ${ICON_SET_DIR}
rm -rf ${GENERATED_MAC_ICON}
mkdir -pv ${ICON_SET_DIR}

cp -pv "${ICON_DIR}/${BASE_NAME}16x16.png"       ${ICON_SET_DIR}/icon_16x16.png
cp -pv "${ICON_DIR}/${BASE_NAME}16x16@2x.png"    ${ICON_SET_DIR}/icon_16x16@2x.png
cp -pv "${ICON_DIR}/${BASE_NAME}32x32.png"       ${ICON_SET_DIR}/icon_32x32.png
cp -pv "${ICON_DIR}/${BASE_NAME}32x32@2x.png"    ${ICON_SET_DIR}/icon_32x32@2x.png
cp -pv "${ICON_DIR}/${BASE_NAME}128x128.png"     ${ICON_SET_DIR}/icon_128x128.png
cp -pv "${ICON_DIR}/${BASE_NAME}128x128@2x.png"  ${ICON_SET_DIR}/icon_128x128@2x.png
cp -pv "${ICON_DIR}/${BASE_NAME}256x256.png"     ${ICON_SET_DIR}/icon_256x256.png
cp -pv "${ICON_DIR}/${BASE_NAME}256x256@2x.png"  ${ICON_SET_DIR}/icon_256x256@2x.png
cp -pv "${ICON_DIR}/${BASE_NAME}512x512.png"     ${ICON_SET_DIR}/icon_512x512.png
cp -pv "${ICON_DIR}/${BASE_NAME}512x512@2x.png"  ${ICON_SET_DIR}/icon_512x512@2x.png


iconutil -c icns ${ICON_SET_DIR}

mv -v VisualDependencies.icns "${ICON_DIR}"
