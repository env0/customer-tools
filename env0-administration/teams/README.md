# Teams Cleanup Tool

this script helps cleanup the teams in your organization that should not be there.

## method 1

mass delete. simply delete all the teams

## method 2 

regex filter. using a filter - we can delete the teams we do not want.
jq -r '.[] | select(.name | test("^foo$")) | .id'
