import org.apache.pdfbox.pdmodel.*;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.*;
import java.util.*;
import org.json.*;

import static java.lang.System.exit;

public class Analyzer {

    public static void main(String[] args) throws IOException, JSONException {
        File jsonFile = new File("pdf.txt");
        PrintWriter writer = new PrintWriter(new FileOutputStream(jsonFile));

        String basePath = "D:/2019spring/searchengine/lab3/Heritrix-new/jobs/TsinghuaNewsV4-20190617091014070/mirror/news.tsinghua.edu.cn/";
        File file = new File(basePath);
        LinkedList<File> list = new LinkedList<File>();
        File[] files = file.listFiles();
        for (File file2 : files) {
            if (file2.isDirectory()) {
//                System.out.println("文件夹:" + file2.getAbsolutePath());
                list.add(file2);
            } else {
//                System.out.println("文件:" + file2.getAbsolutePath());
            }
        }
        File temp_file;
        while (!list.isEmpty()) {
            temp_file = list.removeFirst();
            files = temp_file.listFiles();
            for (File file2 : files) {
                if (file2.isDirectory()) {
                    System.out.println("文件夹:" + file2.getAbsolutePath());
                    list.add(file2);
                } else {
                    String fileName = file2.getName();
                    String suffix = fileName.substring(fileName.lastIndexOf(".") + 1);
                    if(suffix.equals("pdf")){
                        System.out.println(fileName);
                        String content = Extract(file2);
                        String[] segments = content.split("\n");
                        String title;
                        if(segments.length >= 3)
                            title = segments[0]+segments[1]+segments[2];
                        else
                            title = content;
                        title = title.replaceAll("\r", "");
                        title = title.replaceAll("\n", "");
                        String url = file2.getAbsolutePath().substring(111);
                        url = url.replaceAll("\\\\", "/");
                        JSONObject object = new JSONObject();
                        object.put("url", "news.tsinghua.edu.cn/"+url);
                        object.put("title", title);
                        object.put("content",content.replaceAll("\r", "").replaceAll("\n", ""));
                        writer.write(object.toString()+"\n");
                        writer.flush();
                    }
                }
            }
        }
        writer.close();
    }

    static String Extract(File file){
        try {
            //Loading an existing document
            PDDocument document = PDDocument.load(file);

            //Instantiate PDFTextStripper class
            PDFTextStripper pdfStripper = new PDFTextStripper();

            //Retrieving text from PDF document
            String text = pdfStripper.getText(document);

            //Closing the document
            document.close();
            return text;
        }
        catch (IOException e){
        }
        return "";
    }
}
