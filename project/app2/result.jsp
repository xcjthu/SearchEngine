<%@page language="java" contentType="text/html" pageEncoding="UTF-8" %>
<%
String path = request.getContextPath();
String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
%>

<!DOCTYPE HTML >
<html>
<head>
  <base href="<%=basePath%>">

  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>肖特搜索引擎</title>
  <link rel="stylesheet" type="text/css" href="css/style.css" />
</head>
<STYLE>
</STYLE>
<body>
  <%
    String currentQuery=(String) request.getAttribute("currentQuery");
    int currentPage=(Integer) request.getAttribute("currentPage");
  %>
  <div class="dropdown">
    <button class="dropbtn">下拉菜单</button>
    <div class="dropdown-content">
        <a href="imageSearch.jsp">图片搜索</a>
    </div>
  </div>
  <div style="text-align: center">
    <!-- <h1 class="SearchTitle">肖特 Search Engine</h1> -->
    <img class="ResultPageImage" src="img/background.PNG" alt="肖特搜索引擎" />
    <form action="servlet/ImageServer" class="ResultInputForm">
      <input type="search" name="query" style="text-align: left; width: 500px; height: 40px;font-size: 20px" value="<%= currentQuery %>">
      <input type="submit" value="搜索" style="background-color: #007fff; text-align: center; width: 100px; height: 40px;font-size: 20px; color: white; outline-color: #007fff">
    </form>
  <!-- <img src="http://www.w3school.com.cn/i/eg_tulip.jpg"  alt="上海鲜花港 - 郁金香" /> -->
  </div>
  <div>
  </div>
  <div class="ResultBlock">
    <% 
      String[] titles = (String[]) request.getAttribute("Titles");
      String[] contents = (String[]) request.getAttribute("Contents");
      String[] urls = (String[]) request.getAttribute("Urls");
      String formUrl = (String) request.getAttribute("FormUrl");
      String retInfo = (String) request.getAttribute("RetInfo");
      double[] pageRanks = (double[]) request.getAttribute("PageRanks");
      double[] pageScores = (double[]) request.getAttribute("PageScores");
      int len = (int) request.getAttribute("Len");
      String[] pictureUrls = (String[]) request.getAttribute("PictureUrls");
    %>
      <div>
      <%= currentQuery %>
      <%= currentPage %>
      <%= len %>
      </div>
    <%
      for (int i = 0; i < len; ++i){
        %>
        <%= pageRanks[i] %><br>
        <%= pageScores[i] %><br>
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
        <!-- <div>
          <%
          String picture = pictureUrls[i];
          if(picture != null){
          String[] pictures = picture.split(",");
            for(String pic : pictures){
              pic = pic.replaceAll("\\[|\\]|\"| ", "");
              pic = "//"+pic;
              %>
              <img class="SearchResultImg" src="<%= pic %>"  alt="默认图片" />
              <%
            }
          }
          %>
        </div> -->
        <%
      }
    %>
    <br />
    <div>
      <p>
        <%if(currentPage>1){ %>
          <a href="servlet/ImageServer?query=<%=currentQuery%>&page=<%=currentPage-1%>">上一页</a>
        <%}; %>
        <%for (int i=1;i<currentPage;i++){%>
          <a href="servlet/ImageServer?query=<%=currentQuery%>&page=<%=i%>"><%=i%></a>
        <%}; %>
        <strong><%=currentPage%></strong>
        <%for (int i=currentPage+1;i<=5;i++){ %>
          <a href="servlet/ImageServer?query=<%=currentQuery%>&page=<%=i%>"><%=i%></a>
        <%}; %>
        <%if(currentPage<5){ %>
        <a href="servlet/ImageServer?query=<%=currentQuery%>&page=<%=currentPage+1%>">下一页</a>
        <%}; %>
      </p>
    </div>
    <a href="index.jsp">BACK</a> 
  </div>
<body>
</html>