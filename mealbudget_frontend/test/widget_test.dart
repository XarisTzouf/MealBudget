// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

// test/widget_smoke_test.dart
// test/widget_smoke_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mealbudget_frontend/app.dart';

void main() {
  group('MealBudget smoke tests', () {
    testWidgets('app loads', (tester) async {
      await tester.pumpWidget(const MealBudgetApp());

      // ελέγχει ότι άνοιξε το app bar με τον τίτλο
      expect(find.text('MealBudget'), findsOneWidget);
    });

    testWidgets('home screen shows welcome text', (tester) async {
      await tester.pumpWidget(const MealBudgetApp());

      // ελέγχει το βασικό μήνυμα της αρχικής οθόνης
      expect(find.text('Welcome to MealBudget!'), findsOneWidget);
    });
  });
}

