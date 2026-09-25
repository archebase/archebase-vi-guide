import sys
s=open(sys.argv[1] if len(sys.argv)>1 else 'templates/release-report.md').read(); req=['Route:','Artifact:','Source pages/assets:','Asset gate:','Design gate:','Claims/Rights gate:','Export/QA gate:','Verdict:']; miss=[x for x in req if x not in s]; print('FAIL '+str(miss)) if miss else print('PASS release report contract'); sys.exit(bool(miss))
