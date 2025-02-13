import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Guest} from '../guest.interface';
import {AccessibilityOption} from '../accessibility_option.interface';
import {Observable} from 'rxjs';
import {BaseApiService} from './base-api.service';

@Injectable({
  providedIn: 'root'
})
export class GuestService extends BaseApiService {

  public getAllGuests(): Observable<Guest[]> {
    return this.getAll<Guest>("guest/all");
  }

  public getById(id: number): Observable<Guest> {
    return this.get<Guest>(`guest/${id}`);
  }

  public addGuest(guest: Guest, accessibilityOptions: number[]): Observable<Guest> {
    const body = {
      guest: guest,
      accessibility_option_ids: accessibilityOptions.length === 0 ? [-1] : accessibilityOptions,
    }

    return this.post<Guest>("guest/create", body);
  }

  public putGuest(guestId: number, updatedGuest: Guest, accessibilityOptions: number[]): Observable<Guest> {
    const body = {
      updated_guest: updatedGuest,
      new_accessibility_option_ids: accessibilityOptions
    }

    return this.put<Guest>(`guest/${guestId}`, body);
  }

  public deleteGuest(guestId: number): Observable<Object> {
    return this.delete<Object>(`guest/${guestId}`);
  }
}
