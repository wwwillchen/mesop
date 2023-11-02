// Forked from: https://github.com/angular/components/blob/ff67a416d19e9237607605bec0d7cc372025387f/src/dev-app/main.ts
import "@angular/localize/init";

import { importProvidersFrom } from "@angular/core";
import { HttpClientModule } from "@angular/common/http";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { RouterModule } from "@angular/router";
import { bootstrapApplication } from "@angular/platform-browser";

import { App } from "./app";

bootstrapApplication(App, {
  providers: [importProvidersFrom(HttpClientModule)],
});
