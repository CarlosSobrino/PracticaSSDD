// -*- mode:c++ -*-
#include "drobots.ice"

module drobots {

  exception AlreadyExists { string key; };
  exception NoSuchKey { string key; };

  dictionary<string, Object*> ObjectPrxDict;
  dictionary<string, Point> PointPrxDict;
  dictionary<string, int> CoordenadasDict;
  sequence<string> DictKeys;
  sequence<Object*> DictItems;

  interface Container {
    void link(string key, Object* proxy) throws AlreadyExists;
    void linkFactorias(string key, Object* proxy) throws AlreadyExists;
    void linkController(string key, Object* proxy) throws AlreadyExists;
    void linkMinas(string key, Point proxy) throws AlreadyExists;
    void unlink(string key) throws NoSuchKey;
    ObjectPrxDict list();
    ObjectPrxDict listFactorias();
    ObjectPrxDict listController();
    PointPrxDict listMinas();
    Object* get(string key);
    DictKeys keys();
    DictItems items();
    Object* getValueFactorias(int index);
  };

  interface ControllerFactory{

    RobotController* make(Robot* robot, string tipo, string jugador, Container* robotControllerContainer, int indice);

    DetectorController* makeDetector(string tipo, string jugador, Container* robotControllerContainer, int indice);
  };

	interface ControllerAtacante extends RobotController {
		void setRobot(Robot* robot, string jugador,Container* robotControllerContainer);
    Point getPosicionAmiga();
  	};

  interface ControllerDefensor extends RobotController {
		void setRobot(Robot* robot, string jugador,Container* robotControllerContainer);
    Point getPosicionAmiga();
    int getCoordenadaEnemigoX();
    int getCoordenadaEnemigoY();
  	};

  interface ControllerDetector extends DetectorController {
    Point getEnemigo();
    };


 };