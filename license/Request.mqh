//+------------------------------------------------------------------+
//|                                                      Request.mqh |
//|                                     Copyright 2023, Lethan Corp. |
//|                           https://www.mql5.com/pt/users/14134597 |
//+------------------------------------------------------------------+
#property copyright "Copyright 2023, Lethan Corp."
#property link      "https://www.mql5.com/pt/users/14134597"
#property version   "1.00"

#define ERR_HTTP_ERROR_FIRST        ERR_USER_ERROR_FIRST+1000 //+511

#include <JAson.mqh>
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int Request(string method,
            string &out,
            const string url,
            const string payload     = "",
            const string query_param = "",
            string headers           = "",
            const int timeout        = 5000)
  {
   ResetLastError();

   char data[];
   uchar result[];
   string result_headers;
   int res = -1;

   if(method=="GET")
     {
      int data_size=StringLen(query_param);

      if(data_size>0)
        {
         StringToCharArray(query_param, data, 0, data_size);
         res=WebRequest("GET",url +"?"+ query_param, NULL, NULL, timeout, data, data_size, result, result_headers);
        }
      else
        {
         res=WebRequest("GET", url, headers, timeout, data, result, result_headers);
        }
     }

   if(method=="POST")
     {
      ArrayResize(data, StringToCharArray(payload, data, 0, WHOLE_ARRAY)-1);

      if(headers == "")
        {
         headers = "Content-Type: application/json\r\n";
        }

      res=WebRequest("POST",url,headers,timeout,data,result,result_headers);
     }

   if(res==200)//OK
     {
      //--- delete BOM
      int start_index=0;
      int size=ArraySize(result);
      for(int i=0; i<fmin(size,8); i++)
        {
         if(result[i]==0xef || result[i]==0xbb || result[i]==0xbf)
            start_index=i+1;
         else
            break;
        }
      out=CharArrayToString(result,start_index,WHOLE_ARRAY,CP_UTF8);
      return(0);
     }
   else
     {
      if(res==-1)
        {
         return(_LastError);
        }
      else
        {
         //--- HTTP errors
         if(res>=100 && res<=511)
           {
            out=CharArrayToString(result,0,WHOLE_ARRAY,CP_UTF8);
            Print(out);
            return(ERR_HTTP_ERROR_FIRST+res);
           }
         return(res);
        }
     }

   return(0);
  };
//+------------------------------------------------------------------+
