<%@page language="java" contentType="text/html" pageEncoding="UTF-8" %>
<%@page import="java.util.*" %>
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
      <a href="index.jsp">文字搜索</a>
    </div>
  </div>
  <div style="text-align: center">
    <!-- <h1 class="SearchTitle">肖特 Search Engine</h1> -->
    <img class="ResultPageImage" src="img/imagebackground.png" alt="肖特搜索引擎" />
    <form action="servlet/ImageSearchServer" class="ResultInputForm">
      <input type="search" name="query" style="text-align: left; width: 500px; height: 40px;font-size: 20px" value="<%= currentQuery %>">
      <input type="submit" value="搜图" style="background-color: #007fff; text-align: center; width: 100px; height: 40px;font-size: 20px; color: white; outline-color: #007fff">
    </form>
  <!-- <img src="http://www.w3school.com.cn/i/eg_tulip.jpg"  alt="上海鲜花港 - 郁金香" /> -->
  </div>
  <div class="ResultBlock">
    <% 
      ArrayList<String> picUrlList = (ArrayList<String>) request.getAttribute("PicUrlList");
      ArrayList<String> pageUrlList = (ArrayList<String>) request.getAttribute("PageUrlList");
      ArrayList<Integer> widths = (ArrayList<Integer>) request.getAttribute("Widths");
      ArrayList<Integer> heights = (ArrayList<Integer>) request.getAttribute("Heights");
      int len = picUrlList.size();
      for (int i = 0; i < len; ++i){
        String pic = picUrlList.get(i);
        String pageUrl = pageUrlList.get(i);
      %>
        <a href="<%= pageUrl %>">
          <img class="SearchResultImg" src="<%= pic %>"  alt="默认图片" />
        </a>
      <%
      }  
    %>
    <br />
    <div>
      <p>
        <%if(currentPage>1){ %>
          <a href="servlet/ImageSearchServer?query=<%=currentQuery%>&page=<%=currentPage-1%>">上一页</a>
        <%}; %>
        <%for (int i=1;i<currentPage;i++){%>
          <a href="servlet/ImageSearchServer?query=<%=currentQuery%>&page=<%=i%>"><%=i%></a>
        <%}; %>
        <strong><%=currentPage%></strong>
        <%for (int i=currentPage+1;i<=5;i++){ %>
          <a href="servlet/ImageSearchServer?query=<%=currentQuery%>&page=<%=i%>"><%=i%></a>
        <%}; %>
        <%if(currentPage<5){ %>
        <a href="servlet/ImageSearchServer?query=<%=currentQuery%>&page=<%=currentPage+1%>">下一页</a>
        <%}; %>
      </p>
    </div>
    <a href="imageSearch.jsp">BACK</a> 
  </div>
<body>
</html>