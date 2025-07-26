# curl -X GET \
#     localhost:5000/api/users/2/followers?page=1


curl -H 'Content-Type: application/json' \
      -d '{ "username":"Dan123411", "email": "kek11", "password": "111"}' \
      -X PUT \
      localhost:5000/api/users/6

# curl -X GET \
#     localhost:5000/api/hello

