import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-stroke-data-changer',
  templateUrl: './stroke-data-changer.component.html',
  styleUrls: ['./stroke-data-changer.component.css']
})
export class StrokeDataChangerComponent implements OnInit {
  @Input() selected$;
  @Input() strokes$;
  @Output() changeType = new EventEmitter();

  constructor() { }

  ngOnInit() {
  }

}
