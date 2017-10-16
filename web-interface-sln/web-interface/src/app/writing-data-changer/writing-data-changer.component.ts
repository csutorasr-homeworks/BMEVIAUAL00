import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'app-writing-data-changer',
  templateUrl: './writing-data-changer.component.html',
  styleUrls: ['./writing-data-changer.component.css']
})
export class WritingDataChangerComponent implements OnInit {
  @Input() text$: Observable<string>;
  @Input() log$: Observable<string>;

  constructor() { }

  ngOnInit() {
  }

}
