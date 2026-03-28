package com.example.newsindia.service;

import com.example.newsindia.model.NewsItem;
import com.example.newsindia.model.NewsResponse;
import java.time.Instant;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class NewsService {

  private static final Logger logger = LoggerFactory.getLogger(NewsService.class);

  private final RssNewsClient rssNewsClient;
  private final String feedUrl;
  private final long refreshSeconds;

  private volatile CachedNews cached;

  public NewsService(
      RssNewsClient rssNewsClient,
      @Value("${news.rss.url:https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en}") String feedUrl,
      @Value("${news.rss.refresh-seconds:300}") long refreshSeconds
  ) {
    this.rssNewsClient = rssNewsClient;
    this.feedUrl = feedUrl;
    this.refreshSeconds = Math.max(5, refreshSeconds);
  }

  public NewsResponse getCurrentIndiaNews(int limit) {
    int safeLimit = Math.max(1, Math.min(50, limit));
    Instant now = Instant.now();

    CachedNews snapshot = cached;
    if (snapshot != null && now.isBefore(snapshot.fetchedAt.plusSeconds(refreshSeconds))) {
      return new NewsResponse(snapshot.items, null);
    }

    synchronized (this) {
      snapshot = cached;
      if (snapshot != null && now.isBefore(snapshot.fetchedAt.plusSeconds(refreshSeconds))) {
        return new NewsResponse(snapshot.items, null);
      }

      try {
        List<NewsItem> items = rssNewsClient.fetchTopNews(feedUrl, safeLimit);
        cached = new CachedNews(items, Instant.now());
        return new NewsResponse(items, null);
      } catch (Exception e) {
        logger.warn("Failed to fetch RSS news. Serving cached data if available.", e);
        if (cached != null) {
          return new NewsResponse(cached.items, null);
        }
        return new NewsResponse(List.of(), "Could not load current India news at the moment.");
      }
    }
  }

  private static final class CachedNews {
    private final List<NewsItem> items;
    private final Instant fetchedAt;

    private CachedNews(List<NewsItem> items, Instant fetchedAt) {
      this.items = List.copyOf(items);
      this.fetchedAt = fetchedAt;
    }
  }
}

