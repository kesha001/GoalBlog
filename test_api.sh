# curl -X GET \
#     localhost:5000/api/users/2/followers?page=1


# curl -H 'Content-Type: application/json' \
#       -d '{ "username":"Dan123411", "email": "kek11", "password": "111"}' \
#       -X PUT \
#       localhost:5000/api/users/6

# curl -X GET \
#     localhost:5000/api/hello

# curl -X GET \
#     -u "susan:111" \
#     localhost:5000/api/get_token


curl localhost:5000/api/users2 \
   -X GET \
   -H "Accept: application/json" \
   -H "Authorization: Bearer lAYZmBq7dbht8_ZjQHhmEOIZuoy3sQy3l-QC2YFQSBw"

# curl localhost:5000/api/revoke_token \
#    -X DELETE \
#    -H "Accept: application/json" \
#    -H "Authorization: Bearer Ef8leud8YvY18tVNJQvJRw2Fw0NZELYGmMr9MgvverY"