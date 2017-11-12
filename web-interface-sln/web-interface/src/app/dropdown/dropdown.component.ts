import { Component, OnInit, Input, ElementRef } from '@angular/core';

@Component({
  selector: 'app-dropdown',
  templateUrl: './dropdown.component.html',
  styleUrls: ['./dropdown.component.css']
})
export class DropdownComponent implements OnInit {
  @Input() tooltip: string;
  @Input() template: ElementRef;
  show = false;

  constructor() { }

  ngOnInit() {
  }

  toggle() {
    this.show = !this.show;
  }

}
