import { Injectable } from '@angular/core';
import {BaseApiService} from './base-api.service';
import {Observable} from 'rxjs';
import {AccessibilityOption} from '../accessibility_option.interface';

@Injectable({
  providedIn: 'root'
})
export class AccessibilityOptionService extends BaseApiService {

  public getAllAccessibilityOptions(): Observable<AccessibilityOption[]> {
    return this.getAll<AccessibilityOption>("accessibility_option/all");
  }
}
