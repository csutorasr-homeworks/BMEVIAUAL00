import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { WriterComponent } from './writer/writer.component';
import { WriterSelectorComponent } from './writer-selector/writer-selector.component';
import { WritingComponent } from './writing/writing.component';
import { WriterService } from './writer.service';
import { WritingVisualizerComponent } from './writing-visualizer/writing-visualizer.component';
import { ZoomComponent } from './zoom/zoom.component';
import { StrokeDataChangerComponent } from './stroke-data-changer/stroke-data-changer.component';

@NgModule({
  declarations: [
    AppComponent,
    WriterComponent,
    WriterSelectorComponent,
    WritingComponent,
    WritingVisualizerComponent,
    ZoomComponent,
    StrokeDataChangerComponent
  ],
  imports: [
    BrowserModule,
    RouterModule,
    HttpModule,
    AppRoutingModule
  ],
  providers: [
    WriterService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
