package com.example.newsindia.controller;

import com.example.newsindia.model.NewsResponse;
import com.example.newsindia.service.NewsService;
import java.util.Objects;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class NewsController {

  private final NewsService newsService;

  public NewsController(NewsService newsService) {
    this.newsService = Objects.requireNonNull(newsService);
  }

  @GetMapping("/news")
  public ResponseEntity<NewsResponse> getNews(
      @RequestParam(name = "limit", defaultValue = "20") int limit
  ) {
    int safeLimit = Math.max(1, Math.min(50, limit));
    NewsResponse response = newsService.getCurrentIndiaNews(safeLimit);
    if (response.message() != null) {
      return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(response);
    }
    return ResponseEntity.ok(response);
  }
}

