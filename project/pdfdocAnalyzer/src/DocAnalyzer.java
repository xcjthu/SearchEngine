import org.apache.poi.hwpf.HWPFDocument;
import org.apache.poi.hwpf.extractor.WordExtractor;
import org.apache.poi.xwpf.extractor.XWPFWordExtractor;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.*;
import java.util.LinkedList;

public class DocAnalyzer {

    public static void main(String[] args) throws IOException, JSONException {
        File jsonFile = new File("doc.txt");
        PrintWriter writer = new PrintWriter(new FileOutputStream(jsonFile));

        String basePath = "D:/2019spring/searchengine/lab3/Heritrix-new/jobs/TsinghuaNewsV4-20190617091014070/mirror/news.tsinghua.edu.cn";
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
                    if(suffix.equals("doc") || suffix.equals("docx")){
                        System.out.println(fileName);
                        String content;
                        if(suffix.equals("doc"))
                            content = Extract(file2, true);
                        else
                            content = Extract(file2, false);
                        if(content == "") continue;
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

    static String Extract(File file, boolean isDoc){
        try {
            if (isDoc) {
                HWPFDocument document = new HWPFDocument(new FileInputStream(file));
                WordExtractor extractor = new WordExtractor(document);
                return extractor.getText();
            } else {
                XWPFDocument document = new XWPFDocument(new FileInputStream(file));
                XWPFWordExtractor extractor = new XWPFWordExtractor(document);
                return extractor.getText();
            }
        }
        catch (Exception e) {

        }
        return "";
    }
}
