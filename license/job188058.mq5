//+------------------------------------------------------------------+
//|                                                    job188058.mq5 |
//|                                     Copyright 2023, Lethan Corp. |
//|                           https://www.mql5.com/pt/users/14134597 |
//+------------------------------------------------------------------+
#property copyright "Copyright 2023, Lethan Corp."
#property link      "https://www.mql5.com/pt/users/14134597"
#property version   "1.00"
#property script_show_inputs

#include <JAson.mqh>
#include "Request.mqh"

//--- input parameters
input string   username = "user1";
input string   password = "password1";
input int      account_number;

//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
   string out         = "";
   int res            = -1;
   string payload     = "";
   string query_param = "";
   string header      = "";
   int    timeout     = 1000;

   CJAVal json;


   query_param = "server="+ AccountInfoString(ACCOUNT_SERVER) +"&account_number=" + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN), 0);
   res = Request("GET", out, "http://127.0.0.1:8000/metatrader5", payload, query_param, header, timeout);
   if(res == 0)
     {
      json.Deserialize(out);
      Print(json.Serialize());
      // Tratar resultado bem-sucedido aqui
     }
   else
     {
      // Tratar erro aqui
      Print("Deu Ruim!");
     }

   json["username"]       = username;       // login
   json["password"]       = password;       // senha
   json["account_number"] = account_number; // account

//--- serializar para string  {"login":"Login","password":"Pass"}

   payload = json.Serialize();

   res = Request("POST", out, "http://127.0.0.1:8000/login", payload);
   if(res == 0)
     {
      // Tratar resultado bem-sucedido aqui
      Print("Login efetuado com sucesso!");
      json.Deserialize(out);
      Print(json.Serialize());

      header = "Authorization: Bearer " + json["access_token"].ToStr() + "\r\n";

      res = Request("GET", out, "http://127.0.0.1:8000/protected", "", "", header);
      if(res == 0)
        {
         // Tratar resultado bem-sucedido aqui
         Print("Usou o Token para acessar um método protegido");
        }
      else
        {
         // Tratar erro aqui
         Print("Deu Ruim!");
        }
     }
   else
     {
      // Tratar erro aqui
      Print("Deu Ruim!");
     }
  }
//+------------------------------------------------------------------+
