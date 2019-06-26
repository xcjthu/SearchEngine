package mypkg;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.util.Arrays;

public class UserBean {
    String[] contents;
    String[] titles;
    String[] urls;
    int len;
    String formUrl;
    String retInfo;
    String[] pictureUrls;
    double[] pageRanks;
    double[] pageScores;

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

   public String[] getContents(int page){
       return Arrays.copyOfRange(this.contents, 10*(page-1), 10*(page));
   }

    public String[] getTitles(int page){
        return Arrays.copyOfRange(this.titles, 10*(page-1), 10*(page));
    }

    public String[] getUrls(int page){
        return Arrays.copyOfRange(this.urls, 10*(page-1), 10*(page));
    }

    public int getLen(int page){
        int relLen = len-10*(page-1);
        if(relLen > 10) return 10;
        else
            if(relLen > 0) return relLen;
            else return 0;
    }

    public String getFormUrl(){
       return this.formUrl;
    }

    public String getRetInfo(){
       return this.retInfo;
    }

    public String[] getPictureUrls(int page){
       if(pictureUrls != null)
           return Arrays.copyOfRange(this.pictureUrls, 10*(page-1), 10*(page));
       else
           return null;
    }

    public double[] getPageRanks(int page) {
        return Arrays.copyOfRange(this.pageRanks, 10*(page-1), 10*(page));
    }

    public double[] getPageScores(int page) {
        return Arrays.copyOfRange(this.pageScores, 10*(page-1), 10*(page));
    }

    public void SearchResult(String keyword) {
      String urlString = "";
      try
      {
          String originalUrl =  "http://166.111.5.246:20086/search?size=50&where=content&query="+java.net.URLEncoder.encode(keyword, "UTF-8");
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
         this.retInfo = urlString;
          JSONObject jObject = new JSONObject(urlString);
          JSONArray jArray = jObject.getJSONArray("data");
          int len = jArray.length();
          this.len = len;
          contents = new String[len];
          titles = new String[len];
          urls = new String[len];
          pictureUrls = new String[len];
          pageRanks = new double[len];
          pageScores = new double[len];
          for (int i = 0; i < len; i++) {
              JSONObject data = (JSONObject)jArray.get(i);
              JSONObject contents = (JSONObject) data.get("_source");
              pageScores[i] = data.getDouble("_score");
              String content = contents.getString("content");
              String title = contents.getString("title");
              String pageUrl = contents.getString("url");
              pictureUrls[i] = contents.getString("pic_urls");
              pageRanks[i] = contents.getDouble("pageRank");
              pageUrl = "//"+pageUrl;
              this.contents[i] = content.substring(0, 200)+"...";
              this.titles[i] = title;
              this.urls[i] = pageUrl;
          }
      }catch(Exception e)
      {
         e.printStackTrace();
      }
   }
}