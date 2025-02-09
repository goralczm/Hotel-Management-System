import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Guest} from '../guest.interface';
import {AccessibilityOption} from '../accessibility_option.interface';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
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

  public getNGuests(n: number): Guest[] {
    let allGuests: Guest[] = [];
    this.getAllGuests().subscribe((guests) => {
      allGuests = guests;
    });

    if (allGuests.length === 0)
      return [];

    return allGuests.slice(0, n);
  }

  public getAllGuests(): Observable<Guest[]> {
    return this.httpClient.get<Guest[]>(`${this.apiUrl}/guest/all`);
  }

  public getById(id: number): Observable<Guest> {
    return this.httpClient.get<Guest>(`${this.apiUrl}/guest/${id}`);
  }

  public addGuest(guest: Guest, accessibility_options: AccessibilityOption[]): Observable<Guest> {
    const body = {
      guest: guest,
      accessibility_option_ids: accessibility_options.length === 0 ? [-1] : accessibility_options.map<number>(a => a.id),
    }

    return this.httpClient.post<Guest>(`${this.apiUrl}/guest/create`, body);
  }

  public putGuest(guestId: number, updatedGuest: Guest): Observable<Guest> {
    return this.httpClient.put<Guest>(`${this.apiUrl}/guest/${guestId}`, updatedGuest);
  }

  public deleteGuest(guestId: number): Observable<Object> {
    return this.httpClient.delete<Object>(`${this.apiUrl}/guest/${guestId}`);
  }
}
