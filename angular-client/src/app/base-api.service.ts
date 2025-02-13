import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BaseApiService {
  httpClient: HttpClient;
  apiUrl: string;

  constructor(httpClient: HttpClient) {
    this.httpClient = httpClient;
    if (typeof window !== "undefined") {
      this.apiUrl = window.location.hostname === 'localhost'
        ? 'http://localhost:8000'
        : `http://${window.location.hostname}:8000`;
    }
    else
      this.apiUrl = 'http://localhost:8000';
  }

  public get<T>(path: string): Observable<T> {
    return this.httpClient.get<T>(`${this.apiUrl}/${path}`);
  }

  public getAll<T>(path: string): Observable<T[]> {
    return this.httpClient.get<T[]>(`${this.apiUrl}/${path}`);
  }

  public post<T>(path: string, body: {}): Observable<T> {
    return this.httpClient.post<T>(`${this.apiUrl}/${path}`, body);
  }

  public put<T>(path: string, body: {}): Observable<T> {
    return this.httpClient.put<T>(`${this.apiUrl}/${path}`, body);
  }

  public delete<T>(path: string): Observable<T> {
    return this.httpClient.delete<T>(`${this.apiUrl}/${path}`);
  }
}
