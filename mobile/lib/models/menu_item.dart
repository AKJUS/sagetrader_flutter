import 'package:flutter/material.dart';

/*
 * Model: 
 * Single Menu Item Instance for each Tab
*/
class MSPTMenuItem {
  String title;
  IconData icon;
  Widget tab;
  MSPTMenuItem({this.title, this.icon, this.tab});
}

/*
 * Data: 
 * Menu Tabs
*/
List<MSPTMenuItem> menuItems = <MSPTMenuItem>[
  MSPTMenuItem(title: "Trades", icon: Icons.assessment),
  MSPTMenuItem(title: "Strategies", icon: Icons.adjust),
  MSPTMenuItem(title: "Studies", icon: Icons.refresh),
  MSPTMenuItem(title: "T Plan", icon: Icons.work),
  MSPTMenuItem(title: "Tasks", icon: Icons.speaker_notes),
  MSPTMenuItem(title: "Statistics", icon: Icons.trending_up),
];
