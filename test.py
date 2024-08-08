import requests
import json

BASE = "http://127.0.0.1:5000/"

test1_data = {"name": "sesame chicken with sticky asian sauce", 
              "ingredients": {"5 tbsp": "vegetable oil", "2": "eggs lightly beaten", "3 tbsp": "cornstarch", "10 tbsp": "flour",
                              "1/2 tbsp": "salt", "1/2 tbsp": "pepper", "1/2 tbsp": "garlic salt", "2 tbsp": "paprika", 
                              "3": "chicken breasts", "1 tbsp": "sesame oil", "2 cloves": "garlic", "1 tbsp": "rice vinegar",
                              "2 tbsp": "honey", "2 tbsp": "sweet chili sauce", "3 tbsp": "ketchup", "2 tbsp": "brown sugar",
                              "4 tbsp": "soy sauce"}, 
              "instructions": "1: Heat the oil in a wok or large frying pan until very hot. 2: Whilst the oil is heating, \
                place the egg in one shallow bowl and the cornflour in another shallow bowl. Add the flour, salt, pepper, \
                    garlic salt and paprika to another shallow bowl and mix together. Dredge the chicken in the cornflour, \
                        then dip in the egg (make sure all of the chicken is covered in egg wash), and finally dredge \
                            it in the seasoned flour. Add to the wok and cook on a high heat for 6-7 minutes, turning \
                                two or three times during cooking, until well browned. You may need to cook in two batches \
                                    (I find I can do it in one batch so long as it's no more than 3 chicken breasts). \
                                        Remove from the pan and place in a bowl lined with kitchen towels. Add all of the \
                                            sauce ingredients to the hot wok, stir and bubble on a high heat until the sauce \
                                                reduces by about a third (should take 2-3 minutes). Add the chicken back in and \
                                                    toss in the sauce to coat. Cook for 1-2 minutes. Turn off the heat and divide \
                                                        between four bowls. Serve with boiled rice and top with sesame seeds and \
                                                            spring onions."}

response = requests.put(BASE + "recipes/1", 
                        data=json.dumps(test1_data), 
                        headers={'Content-Type': 'application/json'}
                    )
print(response.status_code, response.json())

response = requests.get(BASE)
print(response.status_code, response.json())