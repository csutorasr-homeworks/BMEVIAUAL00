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

@NgModule({
  declarations: [
    AppComponent,
    WriterComponent,
    WriterSelectorComponent,
    WritingComponent
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
