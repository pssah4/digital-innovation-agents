# Codebase-Awareness -- Regeln fuer alle Skills

Jeder Skill MUSS die bestehende Codebase kennen und respektieren.
Kein Artefakt (Dokument, Test, Code, Architektur-Entscheidung) entsteht
im Vakuum -- alles muss im Kontext der realen Codebase funktionieren.

## Vor jeder Arbeit

1. **Bestehenden Code lesen** bevor du Vorschlaege machst oder Dokumente erstellst
2. **Patterns erkennen** die im Projekt etabliert sind (Naming, Struktur, Error Handling)
3. **Abhaengigkeiten verstehen** zwischen Modulen, Services, Tools
4. **Referenz-Implementierung pruefen** falls vorhanden (z.B. forked-kilocode/)

## Fuer Business Analyse & Requirements

- Bestehende Features und deren Implementierung kennen
- Technische Constraints aus der realen Codebase in die Analyse einfliessen lassen
- Scope realistisch einschaetzen basierend auf dem bestehenden Code-Zustand

## Fuer Architecture

- ADR-Vorschlaege muessen zur bestehenden Architektur passen
- Neue Patterns nur vorschlagen wenn sie besser sind als bestehende
- arc42 muss den IST-Zustand korrekt wiedergeben, nicht nur den SOLL

## Fuer Implementierung

- Bestehende Patterns weiterfuehren, nicht neue einfuehren
- Neue Module muessen sich nahtlos integrieren
- Wiring-Pattern des Projekts beachten (Registry, Index, Metadata)

## Fuer Testing

- Bestehende Test-Patterns und Frameworks uebernehmen
- Shared Fixtures und Test-Utilities wiederverwenden
- Test-Konfiguration des Projekts respektieren

## Fuer Security Audit

- Framework-spezifische Security-Patterns beruecksichtigen
- Bestehende Sicherheitsmassnahmen erkennen und wuerdigen
- False Positives im Kontext der Architektur einordnen

## Projekt-Kontext aus CLAUDE.md

Die Projekt-CLAUDE.md im Root-Verzeichnis enthaelt:
- Tech Stack und Build-Befehle
- Projekt-spezifische Regeln (z.B. Obsidian Plugin Review-Bot Rules)
- Referenz-Implementierung Hinweise
- Architektur-Eckdaten

Diese Datei hat VORRANG vor generischen Skill-Anweisungen.
