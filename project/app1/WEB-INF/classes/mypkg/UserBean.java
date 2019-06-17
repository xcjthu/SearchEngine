package mypkg;

import java.net.*;
import java.io.*;
import org.json.*;

public class UserBean {
    String[] contents;
    String[] titles;
    String[] urls;
    int len;
    String formUrl;

   private String username;
 
   public UserBean() {
      username = "";
   }
 
   public String getUsername() {
      return username;
   }
 
   public void setUsername(String username) {
      this.username = username;
   }

   public String[] getContents(){
       return this.contents;
   }

    public String[] getTitles(){
        return this.titles;
    }

    public String[] getUrls(){
        return this.urls;
    }

    public int getLen(){
       return this.len;
    }

    public String getFormUrl(){
       return this.formUrl;
    }

   public void SearchResult(String keyword) {
      String urlString = "";
      try
      {
          String originalUrl =  "http://166.111.5.246:20086/search?where=content&query="+java.net.URLEncoder.encode(keyword, "UTF-8");
          this.formUrl = originalUrl;
         URL url = new URL(this.formUrl);
         URLConnection urlConnection = url.openConnection();
         HttpURLConnection connection = null;
         if(urlConnection instanceof HttpURLConnection)
         {
            connection = (HttpURLConnection) urlConnection;
         }
         else
         {
            System.out.println("url error");
         }
         BufferedReader in = new BufferedReader(
         new InputStreamReader(connection.getInputStream()));
         String current;
         while((current = in.readLine()) != null)
         {
            urlString += current;
         }
          JSONObject jObject = new JSONObject(urlString);
          JSONArray jArray = jObject.getJSONArray("data");
          int len = jArray.length();
          this.len = len;
          contents = new String[len];
          titles = new String[len];
          urls = new String[len];
          for (int i = 0; i < len; i++) {
              JSONObject data = (JSONObject)jArray.get(i);
              JSONObject contents = (JSONObject) data.get("_source");
              String content = contents.getString("content");
              String title = contents.getString("title");
              String pageUrl = contents.getString("url");
              pageUrl = "//"+pageUrl;
              this.contents[i] = content;
              this.titles[i] = title;
              this.urls[i] = pageUrl;
          }
      }catch(Exception e)
      {
         e.printStackTrace();
      }
   }
}