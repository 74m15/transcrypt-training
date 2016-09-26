# -*- coding: utf-8 -*-

from org.transcrypt.stubs.browser import __pragma__

__pragma__("skip")
Trello = 0
__pragma__("noskip")

class pyTrello:
  
  def startup(self):
    print("Eureka!!!")
    
  def do_authenticate(self):
    
    def authenticationSuccess(*args):
      print("authenticationSuccess")
    
    
    def authenticationFailure(*args):
      print("authenticationFailure")
    
    print("do_authenticate")
    
    Trello.authorize({
      "type" : "popup",
      "name": 'Getting Started Application',
      "persist": "false",
      "scope": {
        "read": "true",
        "write": "true" },
      "expiration": "never",
      "success": authenticationSuccess,
      "error": authenticationFailure
    })
  
  
  def do_get_my_cards(self):
    
    card_fields = ["id", "desc", "descData", "due", "email", "name", "subscribed", "url"]
    
    def searchSuccess(data, result, *args):
      print("searchSuccess: {}".format(result))
      
      for item in data.cards:
        for f in card_fields:
          try:
            print("{}: {}".format(f,item[f]))
          except:
            print("no {} property".format(f))
    
    
    def searchFailure(*args):
      print("searchFailure")
      
    print("do_get_my_cards")
    
    Trello.rest(
      "GET",
      "search",
      { "query": "@me", 
        "modelTypes": "cards", 
        "card_fields": ",".join(card_fields),
        "cards_limit": "100"
      },
      searchSuccess,
      searchFailure
    )


trello = pyTrello()