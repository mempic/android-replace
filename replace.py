#!/usr/bin/env python

#
#
# @name mempic.org
# @copyright (c) by SWISS INTERGROUP LP
# @copyright (c) by WWW.MEMPIC.ORG
# @copyright (c) by IGOR MATS
#
#
# @license http://www.mempic.org/licenses/private
#
# By exercising the licensed rights you accept and agree to be bound by the
# terms and conditions of this @license. To the extent this @license
# may be interpreted as a contract, you are granted the licensed rights
# in consideration of your acceptance of these terms and conditions,
# and the licensor grants you such rights in consideration of benefits
# the licensor receives from making the licensed material available
# under these terms and conditions.
#
#
import os
import sys
import argparse
import subprocess
import shutil

def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('file')
    parser.add_argument('keystore')
    parser.add_argument('password')
    parser.add_argument('alias')

    args = vars(parser.parse_args(arguments))
    file = args["file"]
    processPath = os.path.splitext(args["file"])[0]
    keystore = args["keystore"]
    password = args["password"]
    alias = args["alias"]

    if os.path.exists(processPath):
        shutil.rmtree(processPath)
    os.system("apktool d %s" % (file))

    with open(("%s/AndroidManifest.xml" % processPath), 'r+') as content_file:
        content = content_file.read()
        content = content.replace('STRING TO REPLACE', "\n")
        content_file.seek(0)
        content_file.write(content)
        content_file.truncate()

    temp = "%s.tmp" % file
    if os.path.exists(temp):
        os.remove(temp)

    os.system("apktool b %s -o %s" % (processPath, temp))
    shutil.rmtree(processPath)
    success = os.system("jarsigner -strict -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore %s -storepass %s %s %s" % (keystore, password, temp, alias))
    if success != 0:
        sys.exit("signing error")

    result = "%s_signed.apk" % processPath
    if os.path.exists(result):
        os.remove(result)

    os.system("zipalign -v 4 %s %s" % (temp, result))
    os.remove(temp)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
