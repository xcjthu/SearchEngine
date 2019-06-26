<%@page language="java" contentType="text/html" pageEncoding="UTF-8" %>
<!DOCTYPE HTML >
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Echoing HTML Request Parameters</title>
</head>
<STYLE>
</STYLE>
<body>
  <h2>Choose authors:</h2>
  <form method="get">
    <input type="search" name="search">
    <input type="submit" value="Query">
  </form>
  
  <% 
  String[] keywords = request.getParameterValues("search");
  if (keywords != null) {
  %>
    <h3>You are searching for:</h3>
    <ul>
      <%
      for (String keyword : keywords) { 
      %>
        <li><%= keyword %></li>
      <%
      }
      %>
    </ul>
    <jsp:useBean id="user" scope="session" class="mypkg.UserBean" />
    <%    
    String keyword = keywords[0];
    user.SearchResult(keyword);
    String[] titles = user.getTitles();
    String[] contents = user.getContents();
    String[] urls = user.getUrls();
    String formUrl = user.getFormUrl();
    int len = user.getLen();
    for (int i = 0; i < len; ++i){
    %>
      <h3 class="t c-gap-bottom-small">
        <a href=<%= urls[i] %> target="_blank"><%= titles[i] %></a>
      </h3>
      <div class="c-row">
                          <div class="c-span24 c-span-last">
                  <p>
                      <%= contents[i] %>   
                  </p>
          </div>
      </div>   
    <%
    }
  }  
  %>
  <br /><a href="<%= request.getRequestURI() %>">BACK</a> 
  <!-- <div id="content_left">
	

    <div class="result-op c-container xpath-log"  srcid="1547"  id="1" tpl="bk_polysemy" mu="https://baike.baidu.com/item/第三次世界大战/933084" data-op="{'y':'FFDFF3FD'}" data-click="{'p1':'1','rsv_bdr':'0','fm':'albk3',rsv_stl:''}">
                
            <h3 class="t c-gap-bottom-small">
            <a href="http://www.baidu.com/link?url=DQG8HYh1ECtjWs8fJNaOf4jsEMYAVU3ylhTcbKdkEl0xbqdVqKem8LR4H6fiXsYAVwpXiRYHhgEmP32NKCkmOGwVJ_XpYugLpqNrCn680F_Ooqj57MEAFtpxUd7pu8KGPdQl899uJ3-OpTpXbn7kqvuXRCg77TV8XGNAZP4lbAK" target="_blank"><strong>第三次世界大战</strong>_百度百科</a>
            </h3>
            
            
        <div class="c-row">
                            <div class="c-span24 c-span-last">
                    <p>
                        <strong>第三次世界大战</strong>是假想的下一<strong>次世界</strong>的大规模战争，是指两个国家发生了战争，其严重性就可称为是<strong>第三次世界大战</strong>。<strong>世界</strong>各国人民在经历过第一<strong>次世界大战</strong>和第二<strong>次世界</strong>...   
                    </p>
            </div>
                
        </div>   
    </div>
  </div> -->
<body>
</html>