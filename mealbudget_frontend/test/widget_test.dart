

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

