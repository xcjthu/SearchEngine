package mypkg;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.*;

public class ImageSearchServer extends HttpServlet{
	public static final int PAGE_RESULT=10;
	public static final String indexDir="forIndex";
	public static final String picDir="";
	ImageBean imageBean;
	String keyword;

	public ImageSearchServer(){
		super();
		imageBean = new ImageBean();
		keyword = "";
	}
	
	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.setContentType("text/html;charset=utf-8");
		request.setCharacterEncoding("utf-8");
		String queryString=request.getParameter("query");
		String pageString=request.getParameter("page");
		int page=1;
		if(pageString!=null){
			page=Integer.parseInt(pageString);
		}
		if(queryString==null){
			System.out.println("null query");
			//request.getRequestDispatcher("/Image.jsp").forward(request, response);
		}else{
			if(!keyword.equals(queryString)){
				imageBean.SearchResult(queryString);
				keyword = queryString;
			}
			imageBean.setPage(page);
			ArrayList<String> picUrlList = imageBean.getPicUrlList();
			ArrayList<String> pageUrlList = imageBean.getPageUrlList();
			ArrayList<Integer> widths = imageBean.getWidths();
			ArrayList<Integer> heights = imageBean.getHeights();
			request.setAttribute("currentQuery",queryString);
			request.setAttribute("currentPage", page);
			request.setAttribute("PicUrlList", picUrlList);
			request.setAttribute("PageUrlList", pageUrlList);
			request.setAttribute("Widths", widths);
			request.setAttribute("Heights", heights);
			request.getRequestDispatcher("/imageResult.jsp").forward(request,
					response);
		}
	}

	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		this.doGet(request, response);
	}
}
