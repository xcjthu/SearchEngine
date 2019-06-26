package mypkg;

import org.json.JSONArray;
import org.json.JSONObject;

import java.awt.image.BufferedImage;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.Arrays;

public class ImageBean {
    int len;
    String formUrl;
    String retInfo;
    String[] originPicUrls;
    String[] originPageUrls;
    ArrayList<String> picUrlList;
    ArrayList<String> pageUrlList;
    ArrayList<Integer> widths;
    ArrayList<Integer> heights;
    String[] bannedPics;

    private String username;

    public ImageBean() {
        username = "";
        picUrlList = new ArrayList<>();
        pageUrlList = new ArrayList<>();
        widths = new ArrayList<>();
        heights = new ArrayList<>();
        bannedPics = new String[3];
        bannedPics[0] = "www.tsinghua.edu.cn/publish/thunews/images/weixin.jpg";
        bannedPics[1] = "https://www.tsinghua.edu.cn/publish/thunews/images/logo.png";
        bannedPics[2] = "https://www.tsinghua.edu.cn/publish/thunews/images/thulogo.png";
    }

    public int getLen() {
        return len;
    }

    public ArrayList<String> getPicUrlList() {
        return picUrlList;
    }

    public ArrayList<String> getPageUrlList() {
        return pageUrlList;
    }

    public ArrayList<Integer> getWidths() {
        return widths;
    }

    public ArrayList<Integer> getHeights() {
        return heights;
    }

    public void SearchResult(String keyword) {
        picUrlList.clear();
        pageUrlList.clear();
        String urlString = "";
        try
        {
            String originalUrl =  "http://166.111.5.246:20086/search?size=100&where=content&query="+java.net.URLEncoder.encode(keyword, "UTF-8");
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
            originPageUrls = new String[len];
            originPicUrls = new String[len];
            for (int i = 0; i < len; i++) {
                JSONObject data = (JSONObject)jArray.get(i);
                JSONObject contents = (JSONObject) data.get("_source");
                String origins = contents.getString("pic_urls");
                String pageUrl = "//"+contents.getString("url");
                origins = origins.replaceAll("\\[|\\]|\"| ", "");
                originPicUrls[i] = origins;
                originPageUrls[i] = pageUrl;
//                String[] urls = origins.split(",");
//                for (String picUrl : urls) {
//                    if(picUrl.contains(".gif")) continue;
//                    int piclen = getImgLen("https://"+picUrl);
//                    if(piclen > 50000){
//                        picUrlList.add("//" + picUrl);
//                        pageUrlList.add(pageUrl);
//                        widths.add(piclen);
//                        heights.add(piclen);
//                    }
//                }
            }
        }catch(Exception e)
        {
            e.printStackTrace();
        }
    }

    public void setPage(int page){
        picUrlList.clear();
        pageUrlList.clear();
        widths.clear();
        heights.clear();
        String[] pageUrls = Arrays.copyOfRange(originPageUrls, 20*(page-1), 20*page);
        String[] picUrls = Arrays.copyOfRange(originPicUrls, 20*(page-1), 20*page);
        for (int i = 0; i < pageUrls.length; i++) {
            String[] urls = picUrls[i].split(",");
            for (String picUrl : urls) {
                if (picUrl.contains(".gif")) continue;
                int piclen = getImgLen("https://" + picUrl);
                if (piclen > 50000) {
                    picUrlList.add("//" + picUrl);
                    pageUrlList.add(pageUrls[i]);
                    widths.add(piclen);
                    heights.add(piclen);
                }
            }
        }
    }

    public int[] filter(String picUrl){
//        return true;
        int[] arr = getImgWH(picUrl);
        return arr;
//        int width = arr[0];
//        int height = arr[1];
//        if(width < 150 && height < 150)
//            return false;
//        else
//            return true;
    }

    public static int getImgLen(String imgurl) {
        try {
            URL url = new URL(imgurl);

            java.io.BufferedInputStream bis = new BufferedInputStream(url.openStream());

            byte[] bytes = new byte[100];
            int len;
            int count = 0;
            while ((len = bis.read(bytes)) > 0) {
                count += len;
            }
            bis.close();
            return count;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return -1;
    }

    public static int[] getImgWH(String imgurl) {
        boolean b=false;
        String[] segments = imgurl.split("/");
        String filename = segments[segments.length-1];
        try {
            URL url = new URL(imgurl);

            java.io.BufferedInputStream bis = new BufferedInputStream(url.openStream());

            byte[] bytes = new byte[100];

            OutputStream bos = new FileOutputStream(new File(filename));
            int len;
            while ((len = bis.read(bytes)) > 0) {
                bos.write(bytes, 0, len);
            }
            bis.close();
            bos.flush();
            bos.close();

            b=true;
        } catch (Exception e) {

            b=false;
        }
        int[] a = new int[2];
        a[0] = -1;
        a[1] = -1;
        if(b){
            a[0] = -2;
            a[1] = -2;
            java.io.File file = new java.io.File(filename);
            BufferedImage bi = null;
            boolean imgwrong=false;
            try {

                bi = javax.imageio.ImageIO.read(file);
                try{

                    int i = bi.getType();
                    imgwrong=true;
                }catch(Exception e){
                    imgwrong=false;
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
            if(imgwrong){
                a[0] = bi.getWidth();
                a[1] = bi.getHeight();
            }
        }
        return a;
    }

}
