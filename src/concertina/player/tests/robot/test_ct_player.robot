# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s concertina.player -t test_player.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src concertina.player.testing.CONCERTINA_PLAYER_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/concertina/player/tests/robot/test_player.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a player
  Given a logged-in site administrator
    and an add player form
   When I type 'My player' into the title field
    and I submit the form
   Then a player with the title 'My player' has been created

Scenario: As a site administrator I can view a player
  Given a logged-in site administrator
    and a player 'My player'
   When I go to the player view
   Then I can see the player title 'My player'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add player form
  Go To  ${PLONE_URL}/++add++player

a player 'My player'
  Create content  type=player  id=my-player  title=My player

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the player view
  Go To  ${PLONE_URL}/my-player
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a player with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the player title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
