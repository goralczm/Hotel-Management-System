import { TestBed } from '@angular/core/testing';

import { AccessibilityOptionService } from './accessibility-option.service';

describe('AccessibilityOptionService', () => {
  let service: AccessibilityOptionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AccessibilityOptionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
